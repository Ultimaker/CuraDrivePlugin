// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
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

    Image
    {
        id: icon
        anchors.fill: curaDriveDialog
        y: 50
        source: "background.svg"
        fillMode: Image.PreserveAspectCrop
        clip: true
    }

    WelcomePage
    {
        id: welcomePage
        visible: !CuraDrive.isLoggedIn
    }

    BackupsPage
    {
        id: backupsPage
        visible: CuraDrive.isLoggedIn
    }
}
