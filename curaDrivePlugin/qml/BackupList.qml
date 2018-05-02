// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.2
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import UM 1.1 as UM

Item
{
    id: backupList

    property var backups

    anchors.fill: parent

    ScrollView
    {
        frameVisible: false
        anchors.fill: parent
        style: UM.Theme.styles.scrollview

        Column
        {

        }
    }
}