// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import UM 1.3 as UM

import "../components"

RowLayout
{
    id: backupListFooter
    width: parent.width

    ActionButton
    {
        id: createBackupButton
        text: catalog.i18nc("@button", "Backup Now")
        iconSource: "../images/backup.svg"
        enabled: !CuraDrive.isCreatingBackup && !CuraDrive.isRestoringBackup
        onClicked: CuraDrive.createBackup()
    }

    CheckBox
    {
        id: autoBackupEnabled
        checked: CuraDrive.autoBackupEnabled
        text: catalog.i18nc("@checkbox:description", "Auto Backup")
        onClicked: CuraDrive.toggleAutoBackup(autoBackupEnabled.checked)

        hoverEnabled: true
        ToolTip.visible: hovered
        ToolTip.text: catalog.i18nc("@checkbox:description",
            "Automatically create a backup each day that Cura is started.")
    }

//    ActionButton
//    {
//        id: refreshBackupListButton
//        text: catalog.i18nc("@button", "Refresh Backups")
//        iconSource: "../images/restore.svg"
//        color: "transparent"
//        hoverColor: "transparent"
//        textColor: UM.Theme.getColor("text")
//        textHoverColor: UM.Theme.getColor("text_link")
//        enabled: !CuraDrive.isCreatingBackup && !CuraDrive.isRestoringBackup
//        onClicked: CuraDrive.refreshBackups()
//    }
}
