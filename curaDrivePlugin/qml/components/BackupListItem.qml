// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

Rectangle
{
    id: backupListItem
    width: parent.width
    height: showDetails ? dataRow.height + backupDetails.height : dataRow.height
    color: mouseArea.containsMouse ? "#f2f2f2" : "transparent"
    property bool showDetails: false

    // Backup details toggle animation.
    Behavior on height {
        PropertyAnimation {
            duration: 50
        }
    }

    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        onPressed: mouse.accepted = false
        hoverEnabled: true
    }

    RowLayout
    {
        id: dataRow
        spacing: UM.Theme.getSize("default_margin").width * 2
        width: parent.width
        height: 50

        Icon
        {
            width: 32
            source: "../images/folder.svg"
        }

        Label
        {
            text: model["data"]["description"]
            elide: Text.ElideRight
            Layout.minimumWidth: 50
            Layout.maximumWidth: 300
            Layout.fillWidth: true
        }

        Label
        {
            text: model["generated_time"]
            color: "grey"
            elide: Text.ElideRight
            Layout.minimumWidth: 50
            Layout.maximumWidth: 300
            Layout.fillWidth: true
        }

        ActionButton
        {
            color: "transparent"
            hoverColor: "lightgrey"
            iconSource: "../images/info.svg"
            onClicked: backupListItem.showDetails = !backupListItem.showDetails
        }

        ActionButton
        {
            text: "Restore"
            iconSource: "../images/restore.svg"
            enabled: !CuraDrive.isCreatingBackup && !CuraDrive.isRestoringBackup
            onClicked: CuraDrive.restoreBackup(model["backup_id"])
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
