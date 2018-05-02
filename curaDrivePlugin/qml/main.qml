// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.2

import UM 1.3 as UM

Window
{
    id: curaDriveDialog

    minimumWidth: Math.round(UM.Theme.getSize("modal_window_minimum").width)
    minimumHeight: Math.round(UM.Theme.getSize("modal_window_minimum").height)
    width: minimumWidth
    height: minimumHeight

    title: catalog.i18nc("@title:window", "Cura Drive")

    color: "white"

    UM.I18nCatalog
    {
        id: catalog
        name: "cura"
    }

    Column
    {
        id: welcomeView
        spacing: UM.Theme.getSize("default_margin").height * 2
        visible: !CuraDrive.isLoggedIn

         Button
        {
            id: loginButton

            anchors.top: profileDetails.bottom
            visible: !CuraDrive.isLoggedIn

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

    Column
    {
        id: mainView
        spacing: UM.Theme.getSize("default_margin").height * 2
        visible: CuraDrive.isLoggedIn

        ProfileDetails
        {
            id: profileDetails
            profile: CuraDrive.profile
            logoutCallback: CuraDrive.logout
        }

        Rectangle
        {
            id: profileDetailsSpacer
            height: UM.Theme.getSize("default_lining").height
            width: parent.width
            color: UM.Theme.getColor("lining")
        }

        BackupList
        {
            id: backupList
            backups: []
        }
    }
}
