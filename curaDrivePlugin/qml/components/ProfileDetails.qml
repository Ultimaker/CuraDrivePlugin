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
            width: 64
            height: width
            source: profile["profile_image_url"]
        }

        Label
        {
            id: usernameLabel
            text: profile["username"]
            font: UM.Theme.getFont("large")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            Layout.alignment: Qt.AlignLeft
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        ActionButton
        {
            id: logoutButton
            onClicked: profileDetails.logoutCallback()
            text: "Logout"
            Layout.alignment: Qt.AlignRight
        }
    }
}
