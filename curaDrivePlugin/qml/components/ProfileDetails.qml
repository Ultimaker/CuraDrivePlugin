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
            width: 64
            height: width
            source: profile["profile_image_url"]
        }

        Label
        {
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
            onClicked: Qt.openUrlExternally("https://api-staging.ultimaker.com/account/v1/app")
            text: catalog.i18nc("@button", "Manage Profile")
            color: "transparent"
            textColor: UM.Theme.getColor("text")
            iconSource: "../images/home.svg"
            Layout.alignment: Qt.AlignRight
        }

        ActionButton
        {
            onClicked: profileDetails.logoutCallback()
            text: catalog.i18nc("@button", "Sign Out")
            color: "transparent"
            textColor: UM.Theme.getColor("text")
            Layout.alignment: Qt.AlignRight
        }
    }
}
