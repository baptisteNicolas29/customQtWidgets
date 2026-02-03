from typing import List
from Qt import QtWidgets, QtCore, QtGui
import re


class TokenLineEdit(QtWidgets.QLineEdit):

    tokenAdded = QtCore.Signal(str)
    tokenRemoved = QtCore.Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName("TokenLineEdit")

        self._tokens = []
        self._tokensRect = []
        self._hovered_token = None

        self.textChanged.connect(self.onSearchToken)

    def addToken(self, token: str) -> None:
        self._tokens.append(token)
        self.tokenAdded.emit(token)
        self.repaint()

    def removeToken(self, index: int) -> None:
        token = self._tokens.pop(index)
        self.tokenRemoved.emit(token)

        self.repaint()

    def tokens(self) -> List[str]:
        return self._tokens

    def onSearchToken(self, text: str) -> None:
        if not text:
            return

        if text[-1] not in " \t#.,;:!?":
            return

        regex = re.compile(r'#(\w+)([\s#.,;:!?]|$)')
        match = regex.search(text)
        if match:
            # full = match.group(0)   # "#leMot"
            word = match.group(1)   # "leMot"
            self.addToken(word)
            self.blockSignals(True)
            self.setText(re.sub(regex, '', text))
            self.blockSignals(False)

    def paintEvent(self, event):
        super().paintEvent(event)

        self._tokensRect.clear()
        painter = QtGui.QPainter(self)
        palette = self.palette()
        fm = self.fontMetrics()

        prvW = 0
        rect = QtCore.QRect(0, 0, 4, 4)
        for idx, text in enumerate(self._tokens):

            padding = 6
            h = fm.height() + 4
            w = fm.horizontalAdvance(text) + padding * 2

            y = (self.height() - h) // 2
            rect = QtCore.QRect(prvW + 4, y, w, h)
            self._tokensRect.append(rect)

            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            painter.setBrush(palette.highlight())
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(rect, 4, 4)

            painter.setPen(palette.highlightedText().color())
            painter.drawText(rect, QtCore.Qt.AlignCenter, text)
            prvW += w + 4

        self.setTextMargins(rect.width() + rect.x(), 0, 0, 0)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:

        for idx, rect in enumerate(self._tokensRect):
            if rect.contains(event.position().toPoint()):
                self.removeToken(idx)
                break

        return super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if (
            event.key() == QtCore.Qt.Key_Backspace
            and self.cursorPosition() == 0
            and len(self._tokens)
        ):
            self.removeToken(-1)
            # return  # empêche le comportement normal si tu veux

        super().keyPressEvent(event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wdg = TokenLineEdit()
    wdg.setCursorPosition(0)
    wdg.show()
    app.exec()
