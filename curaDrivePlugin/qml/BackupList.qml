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

    ColumnLayout
    {
        spacing: UM.Theme.getSize("default_margin").height * 2

        Repeater
        {
            model: backupList.backups
            delegate: BackupListItem {}
        }
    }
}
