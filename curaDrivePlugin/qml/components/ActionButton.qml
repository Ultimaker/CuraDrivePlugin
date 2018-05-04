// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.1 as UM

Button
{
    id: button
    property alias cursorShape: mouseArea.cursorShape
    property var iconSource: ""
    property var color: UM.Theme.getColor("primary")
    property var hoverColor: UM.Theme.getColor("primary_hover")
    property bool clickable: true

    contentItem: RowLayout
    {
        Icon
        {
            id: buttonIcon
            source: button.iconSource
            width: 16
            visible: button.iconSource != ""
        }

        Text
        {
            id: buttonText
            text: button.text
            color: button.hovered ? UM.Theme.getColor("button_text_hover") : UM.Theme.getColor("button_text")
            font: UM.Theme.getFont("action_button")
            visible: button.text != ""
        }
    }

    background: Rectangle
    {
        color: button.enabled ? (button.hovered ? button.hoverColor : button.color) : "lightgrey"
    }

    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        onPressed: mouse.accepted = false
        hoverEnabled: true
        cursorShape: button.enabled ? (hovered ? Qt.PointingHandCursor : Qt.ArrowCursor) : Qt.ForbiddenCursor
    }
}
