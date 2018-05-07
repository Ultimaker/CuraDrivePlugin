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
        source: "../images/cura_logo.png"
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width / 3
    }

    Label
    {
        id: welcomeTextLabel
        text: catalog.i18nc("@description", "Cura Drive let's you backup and restore your Cura configuration.")
        width: parent.width / 2
        font: UM.Theme.getFont("default")
        color: UM.Theme.getColor("text")
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        wrapMode: Label.WordWrap
    }

    ActionButton
    {
        id: loginButton
        onClicked: CuraDrive.login()
        text: catalog.i18nc("@button", "Sign In")
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
