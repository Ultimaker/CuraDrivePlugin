// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.0

import UM 1.1 as UM

Item
{
    id: profileDetails

    property var profile
    property var logoutCallback

    Row
    {
        id: profileDetailsRow

        spacing: UM.Theme.getSize("default_margin").width * 2

        width: parent.width

        anchors.left: parent.left
        anchors.leftMargin: UM.Theme.getSize("default_margin").width * 3
        anchors.top: parent.top
        anchors.topMargin: UM.Theme.getSize("default_margin").height * 3

        Image
        {
            id: profileImage
            width: 96
            height: 96
            fillMode: Image.PreserveAspectFit
            source: profile.profile_image_url ? profile.profile_image_url : "avatar_default.png"
        }

        Label
        {
            id: usernameLabel
            text: profile.username
            height: 96
            font: UM.Theme.getFont("large")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            anchors.verticalCenter: parent.verticalCenter
        }

        ActionButton
        {
            id: logoutButton
            onClicked: profileDetails.logoutCallback()
            text: "Logout"
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
