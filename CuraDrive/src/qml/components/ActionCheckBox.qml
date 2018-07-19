// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.3 as UM

CheckBox
{
    id: checkbox
    hoverEnabled: true

    property var label: ""

    indicator: Rectangle {
        implicitWidth: 30
        implicitHeight: 30
        x: checkbox.leftPadding
        y: parent.height / 2 - height / 2
        color: UM.Theme.getColor("sidebar")
        border.color: UM.Theme.getColor("text")

        Rectangle {
            width: 14
            height: 14
            x: 8
            y: 8
            color: UM.Theme.getColor("primary")
            visible: checkbox.checked
        }
    }

    contentItem: Label {
        text: catalog.i18nc("@checkbox:description", "Auto Backup")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        verticalAlignment: Text.AlignVCenter
        leftPadding: checkbox.indicator.width + 5
    }

    ActionToolTip
    {
        text: checkbox.label
    }
}
