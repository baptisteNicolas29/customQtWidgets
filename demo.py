import sys
from Qt import QtWidgets
from stepSlider import StepSlider

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    wdg = QtWidgets.QWidget()

    stepSlider = StepSlider(numberOfStep=1)
    startSlider = QtWidgets.QComboBox()
    startSlider.addItems(['Left', 'Center', 'Right'])
    nbrStep = QtWidgets.QSpinBox()
    nbrStep.setMinimum(0)
    nbrStep.setSingleStep(1)

    startSlider.currentIndexChanged.connect(stepSlider.setSliderStartPosition)
    nbrStep.valueChanged.connect(stepSlider.setNumberOfStep)
    # stepSlider.valueChanged.connect(print)

    stepSliderLayout = QtWidgets.QHBoxLayout()
    stepSliderLayout.setContentsMargins(4, 4, 4, 4)
    wdg.setLayout(stepSliderLayout)
    stepSliderLayout.addWidget(stepSlider)
    stepSliderLayout.addWidget(startSlider)
    stepSliderLayout.addWidget(nbrStep)
    wdg.show()
    app.exec()
