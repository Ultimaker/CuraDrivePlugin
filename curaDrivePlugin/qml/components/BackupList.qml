// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.1 as UM

ListView
{
    id: backupList
    property var backups
    width: parent.width
    model: backups
    clip: true
    delegate: BackupListItem {}
    ScrollBar.vertical: RightSideScrollBar {}
}
