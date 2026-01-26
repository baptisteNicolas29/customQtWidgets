from typing import List
from Qt import QtWidgets, QtGui, QtCore


class StepSliderPosition:
    Left = 0
    Middle = 1
    Right = 2


class StepSliderWidget(QtWidgets.QWidget):

    Left = 0
    Middle = 1
    Right = 2

    _SliderInactive = 0
    _SliderSlide = 1
    _SliderStep = 2

    valueChanged = QtCore.Signal(float)

    def __init__(
            self, *args,
            numberOfStep: int = 5,
            sliderPosition=0,
            **kwargs
            ) -> None:

        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setSizePolicy(
                QtWidgets.QSizePolicy.MinimumExpanding,
                QtWidgets.QSizePolicy.Fixed,
                )
        self.__sliderStartPosition = sliderPosition
        self.__numberOfStep = max(1, numberOfStep)

        self.__sliderRect = QtCore.QRect()
        self.__sliderStatus = self._SliderInactive
        self.__mouseFocuseRequested = False

        self.__previousValue = None

    # custom attributes getter/setter
    def numberOfStep(self) -> int:
        return self.__numberOfStep

    def setNumberOfStep(self, value: int) -> None:
        self.__numberOfStep = max(1, value)
        self.repaint()

    def sliderStartPosition(self) -> int:
        return self.__sliderStartPosition

    def setSliderStartPosition(self, value: int) -> None:
        self.__sliderStartPosition = value
        self.repaint()

    # get value emits

    def _getValueToEmit(self) -> float:

        mousePosition = self.mapFromGlobal(QtGui.QCursor.pos())

        if self.__sliderStatus == self._SliderStep:
            rects = self._getGridRect()
            for index, rect in enumerate(rects):
                if rect.left() < mousePosition.x() < rect.right():
                    valueToEmit = float(index) / (len(rects) - 1)

                    if valueToEmit != self.__previousValue:
                        self.valueChanged.emit(valueToEmit)
                        self.__previousValue = valueToEmit
                        return valueToEmit

        elif self.__sliderStatus == self._SliderSlide:
            size = self.size()
            width = size.width()
            height = size.height()
            squareSize = min(width / self.__numberOfStep, height)
            startHeight = (height - squareSize) / 2
            minWidth = 0
            mouseWidth = mousePosition.x() - (squareSize / 2)
            maxWidth = width - squareSize
            sliderRect = QtCore.QRect(
                max(minWidth, min(mouseWidth, maxWidth)),
                startHeight,
                squareSize,
                squareSize
            )
            minRange = sliderRect.width() / 2
            maxRange = width - minRange
            percentage = (mousePosition.x() - minRange) / (maxRange - minRange)
            percentage = max(0, min(percentage, 1))

            if percentage != self.__previousValue:
                self.valueChanged.emit(percentage)
                self.__previousValue = percentage
                return percentage

    # widget graphics methods
    def _getGridSquare(self) -> List[QtCore.QRect]:
        size = self.size()
        width = size.width()
        height = size.height()
        squareSize = min(width / self.__numberOfStep, height)

        startHeight = (height - squareSize) / 2
        widthDivider = width / self.__numberOfStep
        widthOffset = (widthDivider - squareSize) / 2

        squares = []

        for index in range(self.__numberOfStep):
            squares.append(
                QtCore.QRect(
                    (widthDivider * index) + widthOffset,
                    startHeight,
                    squareSize,
                    squareSize,
                )
            )
        return squares

    def _getGridRect(self) -> List[QtCore.QRect]:
        size = self.size()
        width = size.width()
        height = size.height()
        widthDivider = width / self.__numberOfStep
        squares = []

        for index in range(self.__numberOfStep):
            squares.append(
                QtCore.QRect(
                    (widthDivider * index),
                    0,
                    widthDivider,
                    height,
                )
            )
        return squares

    def _paintInactiveMode(
        self,
        painter: QtGui.QPainter,
        gridSquare: List[QtCore.QRect],
        gridRect: List[QtCore.QRect],
        palette: QtGui.QPalette,
    ) -> None:

        mousePosition = None
        if self.__mouseFocuseRequested:
            mousePosition = self.mapFromGlobal(QtGui.QCursor.pos())

        if self.__sliderStartPosition == self.Left:
            sliderIndex = 0

        elif self.__sliderStartPosition == self.Middle:
            sliderIndex = int(self.__numberOfStep / 2)

        else:
            sliderIndex = self.__numberOfStep - 1

        prvBrush = painter.brush()
        for index, (square, rect) in enumerate(zip(gridSquare, gridRect)):

            if mousePosition:
                if rect.contains(mousePosition):
                    painter.setBrush(palette.highlight())

            if index != sliderIndex:
                square -= QtCore.QMargins(
                        square.width() * .2,
                        square.height() * .2,
                        square.width() * .2,
                        square.height() * .2
                        )

            else:
                self.__sliderRect = rect

            painter.drawRect(square)
            painter.setBrush(prvBrush)

    def _paintStepMode(
        self,
        painter: QtGui.QPainter,
        gridSquare: List[QtCore.QRect],
        gridRect: List[QtCore.QRect],
        palette: QtGui.QPalette,
    ) -> None:

        mousePosition = self.mapFromGlobal(QtGui.QCursor.pos())

        prvBrush = painter.brush()
        for index, (square, rect) in enumerate(zip(gridSquare, gridRect)):

            if not rect.left() < mousePosition.x() < rect.right():
                square -= QtCore.QMargins(
                        square.width() * .2,
                        square.height() * .2,
                        square.width() * .2,
                        square.height() * .2
                        )
            else:
                painter.setBrush(palette.highlight())
                self.__sliderRect = rect

            painter.drawRect(square)
            painter.setBrush(prvBrush)

    def _paintSlideMode(
        self,
        painter: QtGui.QPainter,
        gridSquare: List[QtCore.QRect],
        gridRect: List[QtCore.QRect],
        palette: QtGui.QPalette,
    ) -> None:

        mousePosition = self.mapFromGlobal(QtGui.QCursor.pos())
        size = self.size()
        width = size.width()
        height = size.height()
        squareSize = min(width / self.__numberOfStep, height)
        startHeight = (height - squareSize) / 2
        minWidth = 0
        mouseWidth = mousePosition.x() - (squareSize / 2)
        maxWidth = width - squareSize

        sliderRect = QtCore.QRect(
            max(minWidth, min(mouseWidth, maxWidth)),
            startHeight,
            squareSize,
            squareSize
        )
        self.__sliderRect = QtCore.QRect(
            max(minWidth, min(mouseWidth, maxWidth)),
            0,
            squareSize,
            height,
        )

        prvBrush = painter.brush()
        painter.setBrush(palette.highlight())
        painter.drawRect(sliderRect)
        painter.setBrush(prvBrush)

        # compute bounding rect for text
        sizeLeft = self.__sliderRect.left()
        sizeRight = width - self.__sliderRect.right()
        painter.setPen(palette.text().color())

        minRange = sliderRect.width() / 2
        maxRange = width - minRange
        percentage = (mousePosition.x() - minRange) / (maxRange - minRange)
        percentage = max(0, min(percentage, 1))

        if sizeLeft > sizeRight:
            textRect = QtCore.QRect(
                0,
                0,
                sizeLeft,
                height,
            )

        else:
            textRect = QtCore.QRect(
                self.__sliderRect.right(),
                0,
                sizeRight,
                height,
            )

        painter.drawText(
            textRect,
            QtCore.Qt.AlignCenter,
            str(round(percentage, 3))
        )

        painter.setPen(QtCore.Qt.NoPen)

    # override events
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:

        palette = self.palette()
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(palette.base())
        painter.setPen(QtCore.Qt.NoPen)

        gridSquare = self._getGridSquare()
        gridRect = self._getGridRect()

        if self.__sliderStatus == self._SliderInactive:
            self._paintInactiveMode(painter, gridSquare, gridRect, palette)

        elif self.__sliderStatus == self._SliderStep:
            self._paintStepMode(painter, gridSquare, gridRect, palette)

        else:
            self._paintSlideMode(painter, gridSquare, gridRect, palette)

        painter.end()
        super().paintEvent(event)

    def enterEvent(self, event) -> None:
        self.__mouseFocuseRequested = True
        super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.__mouseFocuseRequested = False
        self.repaint()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.repaint()

        value = self._getValueToEmit()
        if value is not None:
            self.valueChanged.emit(value)

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.__sliderRect.contains(event.pos()):
            self.__sliderStatus = self._SliderSlide

        else:
            self.__sliderStatus = self._SliderStep

        self.repaint()

        value = self._getValueToEmit()
        if value is not None:
            self.valueChanged.emit(value)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.__sliderStatus = self._SliderInactive
        self.repaint()

        value = self._getValueToEmit()
        if value is not None:
            print(f'mouthReleaseEvent emit: {value}')
            self.valueChanged.emit(value)

        self.__previousValue = None

        super().mouseReleaseEvent(event)

    # override Qt methods
    def minimumSizeHint(self) -> None:

        fontMetric = QtGui.QFontMetrics(self.font())

        return QtCore.QSize(
                self.__numberOfStep * fontMetric.height(),
                fontMetric.height()
                )
