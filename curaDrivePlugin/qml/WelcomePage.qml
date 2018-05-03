// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Window 2.2

import UM 1.3 as UM

Column
{
    id: welcomePage
    spacing: UM.Theme.getSize("default_margin").height * 2
    width: parent.width
    topPadding: 150

    Image
    {
        id: profileImage
        fillMode: Image.PreserveAspectFit
        source: "cura_logo.png"
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width / 3
    }

    Label
    {
        id: welcomeTextLabel
        text: "Welcome to Cura Drive. If you log in using your Ultimaker account, you can backup and restore your Cura configurations!"
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
        text: "Login"
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
