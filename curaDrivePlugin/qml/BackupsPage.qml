// Copyright (c) 2018 Ultimaker B.V.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.2

import UM 1.3 as UM

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

    BackupList
    {
        id: backupList
        backups: []
    }
}
