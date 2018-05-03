// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.3 as UM

ColumnLayout
{
    id: backupsPage
    spacing: UM.Theme.getSize("default_margin").height * 2
    width: parent.width
    height: parent.height

    ProfileDetails
    {
        id: profileDetails
        profile: CuraDrive.profile
        logoutCallback: CuraDrive.logout
        Layout.fillWidth: true
        Layout.preferredHeight: childrenRect.height + 40
    }

    Label
    {
        id: backupTitle
        text: "My Backups"
        font: UM.Theme.getFont("large")
        color: UM.Theme.getColor("text")
        Layout.fillWidth: true
        Layout.preferredHeight: 40
        padding: UM.Theme.getSize("default_margin").width * 2
    }

    BackupList
    {
        id: backupList
        backups: CuraDrive.backups
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredHeight: 300
    }
}
