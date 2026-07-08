"""
POS App Views Package
"""
from .terminal_wizard import (
    TerminalWizardStep1View,
    TerminalWizardStep2View,
    TerminalWizardStep3View,
    TerminalWizardStep4View,
    TerminalWizardStep5View,
)
from .reader_wizard import (
    ReaderWizardStep1View,
    ReaderWizardStep2View,
    ReaderWizardStep3View,
)

__all__ = [
    # Terminal Provider Wizard
    'TerminalWizardStep1View',
    'TerminalWizardStep2View',
    'TerminalWizardStep3View',
    'TerminalWizardStep4View',
    'TerminalWizardStep5View',
    # Reader Wizard
    'ReaderWizardStep1View',
    'ReaderWizardStep2View',
    'ReaderWizardStep3View',
]
