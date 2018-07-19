// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.3 as UM

RowLayout
{
    id: detailsRow
    width: parent.width
    height: 40

    property var iconSource
    property var label
    property var value

    // Spacing.
    Item
    {
        width: 40
    }

    Icon
    {
        width: 18
        iconSource: detailsRow.iconSource
        color: UM.Theme.getColor("text")
    }

    Label
    {
        text: detailsRow.label
        color: UM.Theme.getColor("text")
        elide: Text.ElideRight
        Layout.minimumWidth: 50
        Layout.maximumWidth: 100
        Layout.fillWidth: true
        renderType: Text.NativeRendering
    }

    Label
    {
        text: detailsRow.value
        color: UM.Theme.getColor("text")
        elide: Text.ElideRight
        Layout.minimumWidth: 50
        Layout.maximumWidth: 100
        Layout.fillWidth: true
        renderType: Text.NativeRendering
    }
}
