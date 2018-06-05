// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Window 2.2

import UM 1.3 as UM

import "../components"

Column
{
    id: welcomePage
    spacing: UM.Theme.getSize("wide_margin").height
    width: parent.width
    topPadding: 150

    Image
    {
        id: profileImage
        fillMode: Image.PreserveAspectFit
        source: "../images/icon.png"
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width / 4
    }

    Label
    {
        id: welcomeTextLabel
        text: catalog.i18nc("@description", "Backup and synchronize your Cura settings.")
        width: parent.width / 2
        font: UM.Theme.getFont("default")
        color: UM.Theme.getColor("text")
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        anchors.horizontalCenter: parent.horizontalCenter
        wrapMode: Label.WordWrap
        renderType: Text.NativeRendering
    }

    ActionButton
    {
        id: loginButton
        onClicked: CuraDrive.login()
        text: catalog.i18nc("@button", "Sign In")
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
