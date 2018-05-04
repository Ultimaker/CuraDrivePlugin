// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1

import UM 1.1 as UM

Button
{
    id: button
    property alias cursorShape: mouseArea.cursorShape
    property var iconSource
    property var color: UM.Theme.getColor("primary")
    property var hoverColor: UM.Theme.getColor("primary_hover")

    contentItem: Text
    {
        id: buttonText
        text: button.text
        color: button.hovered ? UM.Theme.getColor("button_text_hover") : UM.Theme.getColor("button_text")
        font: UM.Theme.getFont("action_button")
    }

    background: Rectangle
    {
        color: button.hovered ? button.hoverColor : button.color
    }

    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        onPressed: mouse.accepted = false
        hoverEnabled: true
        cursorShape: hovered ? Qt.PointingHandCursor : Qt.ArrowCursor
    }
}
