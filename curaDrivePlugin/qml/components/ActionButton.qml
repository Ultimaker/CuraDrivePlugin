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
    property var disabledColor: UM.Theme.getColor("button_disabled")
    property var textColor: UM.Theme.getColor("button_text")
    property var textHoverColor: UM.Theme.getColor("button_text_hover")
    property var textFont: UM.Theme.getFont("action_button")

    contentItem: RowLayout
    {
        Icon
        {
            id: buttonIcon
            iconSource: button.iconSource
            width: 16
            color: button.hovered ? button.textHoverColor : button.textColor
            visible: button.iconSource != ""
        }

        Label
        {
            id: buttonText
            text: button.text
            color: button.hovered ? button.textHoverColor : button.textColor
            font: button.textFont
            visible: button.text != ""
        }
    }

    background: Rectangle
    {
        color: button.enabled ? (button.hovered ? button.hoverColor : button.color) : button.disabledColor
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
