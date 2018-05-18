// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1

import UM 1.1 as UM

Item
{
    id: backupListItem
    width: parent.width
    height: showDetails ? dataRow.height + backupDetails.height : dataRow.height
    property bool showDetails: false

    // Backup details toggle animation.
    Behavior on height
    {
        PropertyAnimation
        {
            duration: 70
        }
    }

    RowLayout
    {
        id: dataRow
        spacing: UM.Theme.getSize("default_margin").width * 2
        width: parent.width
        height: 50

        ActionButton
        {
            color: "transparent"
            hoverColor: "transparent"
            textColor: UM.Theme.getColor("text")
            textHoverColor: UM.Theme.getColor("primary")
            iconSource: "../images/info.svg"
            onClicked: backupListItem.showDetails = !backupListItem.showDetails
        }

        Label
        {
            text: new Date(model["generated_time"]).toLocaleString(UM.Preferences.getValue("general/language"))
            elide: Text.ElideRight
            Layout.minimumWidth: 100
            Layout.maximumWidth: 500
            Layout.fillWidth: true
        }

        Label
        {
            text: model["data"]["description"]
            elide: Text.ElideRight
            Layout.minimumWidth: 100
            Layout.maximumWidth: 500
            Layout.fillWidth: true
        }

        ActionButton
        {
            text: catalog.i18nc("@button", "Restore")
            color: "transparent"
            hoverColor: "transparent"
            textColor: UM.Theme.getColor("text")
            textHoverColor: UM.Theme.getColor("text_hover")
            enabled: !CuraDrive.isCreatingBackup && !CuraDrive.isRestoringBackup
            onClicked: confirmRestoreDialog.visible = true
        }

        ActionButton
        {
            color: "transparent"
            hoverColor: "transparent"
            textColor: UM.Theme.getColor("setting_validation_error_background")
            textHoverColor: UM.Theme.getColor("setting_validation_error_background")
            iconSource: "../images/delete.svg"
            onClicked: confirmDeleteDialog.visible = true
        }
    }

    BackupListItemDetails
    {
        id: backupDetails
        backupDetailsData: model
        width: parent.width
        visible: parent.showDetails
        anchors.top: dataRow.bottom
    }

    MessageDialog
    {
        id: confirmDeleteDialog
        title: catalog.i18nc("@dialog:title", "Delete Backup")
        text: catalog.i18nc("@dialog:info", "Are you sure you want to delete this backup? This cannot be undone.")
        standardButtons: StandardButton.Yes | StandardButton.No
        onYes: CuraDrive.deleteBackup(model["backup_id"])
    }

    MessageDialog
    {
        id: confirmRestoreDialog
        title: catalog.i18nc("@dialog:title", "Restore Backup")
        text: catalog.i18nc("@dialog:info", "Cura will restart after your backup has been restored. Continue?")
        standardButtons: StandardButton.Yes | StandardButton.No
        onYes: CuraDrive.restoreBackup(model["backup_id"])
    }
}
