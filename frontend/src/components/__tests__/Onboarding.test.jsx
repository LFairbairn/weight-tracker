import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import Onboarding from '../Onboarding'

describe('Onboarding', () => {
  it('renders the heading and file inputs', () => {
    render(<Onboarding onComplete={vi.fn()} />)

    expect(screen.getByText('Welcome to Weight Tracker')).toBeInTheDocument()
    expect(screen.getByLabelText('User data (user.csv)')).toBeInTheDocument()
    expect(screen.getByLabelText('Weight log (weight_log.csv)')).toBeInTheDocument()
    expect(screen.getByLabelText('Medication doses (medication_doses.csv)')).toBeInTheDocument()
  })

  it('renders the submit button', () => {
    render(<Onboarding onComplete={vi.fn()} />)

    expect(screen.getByRole('button', { name: 'Upload & Get Started' })).toBeInTheDocument()
  })
})
