// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Window 2.2

import UM 1.3 as UM

import "components"
import "pages"

Window
{
    id: curaDriveDialog
    minimumWidth: Math.round(UM.Theme.getSize("modal_window_minimum").width)
    minimumHeight: Math.round(UM.Theme.getSize("modal_window_minimum").height)
    maximumWidth: minimumWidth * 1.2
    maximumHeight: minimumHeight * 1.2
    width: minimumWidth
    height: minimumHeight
    color: "white"
    title: catalog.i18nc("@title:window", "Cura Drive")

    // Globally available.
    UM.I18nCatalog
    {
        id: catalog
        name: "cura_drive"
    }

    Image
    {
        id: icon
        anchors.fill: curaDriveDialog
        y: 50
        source: "images/background.svg"
        fillMode: Image.PreserveAspectCrop
        clip: true
    }

    Image
    {
        id: previewBanner
        source: "images/preview_banner.png"
        width: 96
        height: width
        x: curaDriveDialog.width - width
        y: 0
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
