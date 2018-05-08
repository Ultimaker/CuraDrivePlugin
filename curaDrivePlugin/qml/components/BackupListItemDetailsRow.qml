// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

RowLayout
{
    id: detailsRow
    width: parent.width
    height: 40

    property var iconSource
    property var label
    property var value

    Icon
    {
        width: 24
        iconSource: detailsRow.iconSource
    }

    Label
    {
        text: detailsRow.label
        elide: Text.ElideRight
        Layout.minimumWidth: 50
        Layout.maximumWidth: 100
        Layout.fillWidth: true
    }

    Label
    {
        text: detailsRow.value
        elide: Text.ElideRight
        Layout.minimumWidth: 50
        Layout.maximumWidth: 100
        Layout.fillWidth: true
    }
}
