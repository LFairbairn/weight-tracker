from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from scipy.stats import linregress
from datetime import timedelta
from app.database import get_db
from app.deps import get_current_user
from app.models.weight_log import WeightLog
from app.models.medication_dose import MedicationDose


router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("")
def get_stats(db: Session = Depends(get_db)):
    user = get_current_user(db)
    logs = (
        db.query(WeightLog)
        .filter(WeightLog.user_id == user.id)
        .order_by(WeightLog.date)
        .all()
    )

    doses = (
        db.query(MedicationDose)
        .order_by(MedicationDose.date_changed)
        .all()
    )

    last_log_date = logs[-1].date
    dose_periods = []

    for i, dose in enumerate(doses):
        start = dose.date_changed
        # end date is day before next dose, or last log date if this is the last dose
        end = doses[i + 1].date_changed - timedelta(days=1) if i + 1 < len(doses) else last_log_date

        # filter logs that fall within this period and have a weight value
        period_logs = [l for l in logs if start <= l.date <= end and l.weight_kg is not None]

        if len(period_logs) < 2:
            # can't do regression with fewer than 2 points
            dose_periods.append({
                "dose": dose.dose,
                "unit": dose.unit,
                "start_date": str(start),
                "end_date": str(end),
                "entries": len(period_logs),
                "slope_kg_per_week": None,
                "r_squared": None,
            })
            continue

        # convert dates to weeks since start of this period
        x = [(l.date - start).days / 7 for l in period_logs]
        y = [l.weight_kg for l in period_logs]

        result = linregress(x, y)

        dose_periods.append({
            "dose": dose.dose,
            "unit": dose.unit,
            "start_date": str(start),
            "end_date": str(end),
            "entries": len(period_logs),
            "slope_kg_per_week": round(result.slope, 3),
            "r_squared": round(result.rvalue ** 2, 3),
            "intercept": round(result.intercept, 3),
        })

    # overall trend across all logs
    all_x = [(l.date - logs[0].date).days / 7 for l in logs if l.weight_kg is not None]
    all_y = [l.weight_kg for l in logs if l.weight_kg is not None]
    overall = linregress(all_x, all_y)

    return {
        "dose_periods": dose_periods,
        "overall": {
            "slope_kg_per_week": round(overall.slope, 3),
            "r_squared": round(overall.rvalue ** 2, 3),
        }
    }

