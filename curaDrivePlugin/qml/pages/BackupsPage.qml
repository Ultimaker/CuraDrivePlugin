// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.3 as UM

import "../components"

Item
{
    id: backupsPage
    anchors.fill: parent
    anchors.margins: UM.Theme.getSize("default_margin").width * 3

    ColumnLayout
    {
        spacing: UM.Theme.getSize("default_margin").height * 2
        width: parent.width
        anchors.fill: parent

        ProfileDetails
        {
            id: profileDetails
            profile: CuraDrive.profile
            logoutCallback: CuraDrive.logout
            Layout.fillWidth: true
        }

        Divider
        {
            width: parent.width
            Layout.fillWidth: true
        }

        Label
        {
            id: backupTitle
            text: "My Backups"
            font: UM.Theme.getFont("large")
            color: UM.Theme.getColor("text")
            Layout.fillWidth: true
        }

        BackupList
        {
            id: backupList
            backups: CuraDrive.backups
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        ActionButton
        {
            id: createBackupButton
            text: "Backup now"
            iconSource: "../images/backup.svg"
            enabled: !CuraDrive.isCreatingBackup && !CuraDrive.isRestoringBackup
            onClicked: CuraDrive.createBackup()
        }
    }
}
