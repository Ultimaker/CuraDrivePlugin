// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

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
            onClicked: CuraDrive.restoreBackup(model["backup_id"])
        }

        ActionButton
        {
            color: "transparent"
            hoverColor: "transparent"
            textColor: UM.Theme.getColor("setting_validation_error_background")
            textHoverColor: UM.Theme.getColor("setting_validation_error_background")
            iconSource: "../images/delete.svg"
            onClicked: CuraDrive.deleteBackup(model["backup_id"])
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
}
