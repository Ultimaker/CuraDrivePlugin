// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.1 as UM

Item
{
    id: backupList
    property var backups
    height: childrenRect.height

    ListView
    {
        width: parent.width
        height: childrenRect.height
        model: backupList.backups
        delegate: BackupListItem {}
    }
}
