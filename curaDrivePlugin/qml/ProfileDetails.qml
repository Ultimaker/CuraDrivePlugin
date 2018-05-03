// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.0

import UM 1.1 as UM

Item
{
    id: profileDetails
    property var profile
    property var logoutCallback
    height: childrenRect.height

    RowLayout
    {
        id: profileDetailsRow
        spacing: UM.Theme.getSize("default_margin").width * 2
        width: parent.width

        AvatarImage
        {
            id: profileImage
            width: 96
            height: width
            source: profile["profile_image_url"]
            Layout.alignment: Qt.AlignLeft
        }

        Label
        {
            id: usernameLabel
            text: profile["username"]
            height: 96
            font: UM.Theme.getFont("large")
            color: UM.Theme.getColor("text")
            Layout.alignment: Qt.AlignLeft
        }

        ActionButton
        {
            id: logoutButton
            onClicked: profileDetails.logoutCallback()
            text: "Logout"
            anchors.verticalCenter: parent.verticalCenter
            Layout.alignment: Qt.AlignRight
        }
    }
}
