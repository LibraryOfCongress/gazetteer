/*
    Maps URLs to function calls defined in controller.js
*/

define(['marionette', 'app/settings', 'app/core/controller'], function(Marionette, settings, GazController) {
    var appRoutes = {};
    var appBase = GAZETTEER_APP_BASE; //FIXME: for some reason, was unable to access settings.app_base, please use that if possible
    appBase = appBase.substring(1, appBase.length); //remove initial slash from appBase
    appRoutes[appBase + 'search'] = 'search';
    appRoutes[appBase + 'place/:id'] = 'detail';
    appRoutes[appBase + 'place/:id/:tab'] = 'detail'; 
    console.log(appRoutes);
    var router = Marionette.AppRouter.extend({
        controller: GazController,
        appRoutes: appRoutes
/*        {
            '': 'home',
            settings.APP_BASE + 'search': 'search',
            settings.APP_BASE + 'place/:id': 'detail',
            settings.APP_BASE + 'place/:id/:tab': 'detail'
        } */
    });
    return router;
});
