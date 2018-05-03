// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.1 as UM

Rectangle
{
    id: backupListItem
    height: childrenRect.height
    width: parent.width
    color: mouseArea.containsMouse ? "#f2f2f2" : "transparent"

    RowLayout
    {
        id: dataRow
        spacing: UM.Theme.getSize("default_margin").width * 2
        width: parent.width
        height: 50

        Label
        {
            text: model["backup_id"]
            elide: Text.ElideRight
            Layout.minimumWidth: 50
            Layout.maximumWidth: 300
            Layout.fillWidth: true
        }

        Label
        {
            text: model["generated_time"]
            elide: Text.ElideRight
            Layout.minimumWidth: 50
            Layout.maximumWidth: 300
            Layout.fillWidth: true
        }
    }

    Divider
    {
        anchors.bottom: parent.bottom
        width: parent.width
    }

    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        onPressed: mouse.accepted = false
        hoverEnabled: true
    }
}
