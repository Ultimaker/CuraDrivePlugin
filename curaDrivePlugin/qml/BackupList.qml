// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1

import UM 1.1 as UM

Item
{
    id: backupList
    property var backups
    anchors.fill: parent

    Column
    {
        id: backupListLayout
        height: childrenRect.height * 2

        Repeater
        {
            model: backupList.backups
            delegate: BackupListItem {}
        }
    }
}
