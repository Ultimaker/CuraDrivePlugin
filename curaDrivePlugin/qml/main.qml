// Copyright (c) 2018 Ultimaker B.V.
// Cura is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Controls.Styles 1.4

import UM 1.3 as UM

UM.Dialog
{
    id: curaDriveDialog

    minimumWidth: Math.round(UM.Theme.getSize("modal_window_minimum").width * 0.75)
    minimumHeight: Math.round(UM.Theme.getSize("modal_window_minimum").height * 0.5)
    width: minimumWidth
    height: minimumHeight

    title: catalog.i18nc("@title:window", "Cura Drive")

    Item
    {
        // UM.I18nCatalog must be wrapped in an item.
        UM.I18nCatalog
        {
            id: catalog
            name:"cura"
        }

        // Ensure the Item is always the same size as the whole Dialog.
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            bottom: parent.bottom
        }

        Label
        {
            id: usernameLabel
            text: CuraDrive.profile.username

            width: parent.width
            height: 50
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
        }

        Label
        {
            id: accessTokenLabel
            text: CuraDrive.token.access_token

            width: parent.width
            height: 50
            anchors.top: usernameLabel.bottom
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
        }

        Button
        {
            id: loginButton

            anchors.top: accessTokenLabel.bottom

            onClicked: CuraDrive.login()

            contentItem: Text {
                id: loginButtonText
                text: "Login"
                color: UM.Theme.getColor("action_button_text")
                font: UM.Theme.getFont("action_button")
            }

            background: Rectangle {
                color: UM.Theme.getColor("action_button")
            }
        }
    }
}
