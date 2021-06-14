<template>
  <div>
    <h2>{{$t('settings.configuration')}}</h2>
    <div v-if="!view.isLoaded" class="spinner spinner-lg"></div>
    <div v-if="view.isLoaded">
      <form class="form-horizontal" v-on:submit.prevent="saveSettings('status')">
        <div :class="['form-group', errors.status.hasError ? 'has-error' : '']">
              <label
                class="col-sm-2 control-label"
                for="textInput-modal-markup"
              >{{$t('settings.status')}}</label>
              <div class="col-sm-5">
                <toggle-button
                  class="min-toggle"
                  :width="40"
                  :height="20"
                  :color="{checked: '#0088ce', unchecked: '#bbbbbb'}"
                  :value="configuration.status"
                  :sync="true"
                  @change="toggleStatus()"
                />
                <span
                  v-if="errors.status.hasError"
                  class="help-block"
                >{{errors.status.message}}</span>
              </div>
        </div>
        <div
          v-if="configuration.status"
          :class="['form-group', errors.Webaccess.hasError ? 'has-error' : '']"
        >
          <label
            class="col-sm-2 control-label"
            for="textInput-modal-markup"
          >{{$t('settings.Webaccess')}}</label>
          <div class="col-sm-5">
            <input type="checkbox"   true-value="public" false-value="private" v-model="configuration.Webaccess" class="form-control">
            <span
              v-if="errors.Webaccess.hasError"
              class="help-block"
            >{{errors.Webaccess.message}}</span>
          </div>
        </div>
        <div 
          v-if="configuration.status"
          :class="['form-group', errors.Users.hasError ? 'has-error' : '']">
          <label
            class="col-sm-2 control-label"
            for="textInput-modal-markup"
          >{{$t('settings.Users')}}
          </label>
          <div class="col-sm-5">
            <textarea rows="5" v-model="configuration.Users" class="form-control"></textarea>
            <span v-if="errors.Users.hasError" class="help-block">
              {{$t('validation.validation_failed')}}:
              {{$t('validation.'+errors.Users.message)}}: {{errors.Users.value}}
            </span>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-2 control-label" for="textInput-modal-markup">
            <div v-if="loaders" class="spinner spinner-sm form-spinner-loader adjust-top-loader"></div>
          </label>
          <div class="col-sm-5">
            <button class="btn btn-primary" type="submit">{{$t('save')}}</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Settings",
  components: {
  },
  mounted() {
    this.getSettings();
  },
  beforeRouteLeave(to, from, next) {
    $(".modal").modal("hide");
    next();
  },
  data() {
  return {
    view: {
      isLoaded: false
    },
    loaders: false,
    errors: this.initErrors()
  };
},
methods: {
  initErrors() {
    return {
      status: {
        hasError: false,
        message: ""
      },
      Webaccess: {
        hasError: false,
        message: ""
      },
      Users: {
          haserror: false,
          message:""
      }
    };
  },
  getSettings() {
    var context = this;
    context.view.isLoaded = false;
    context.advanced = false;
    
    nethserver.exec(
      ["nethserver-transmission/read"],
      {
        action: "configuration"
      },
      null,
      function(success) {
        try {
          success = JSON.parse(success);
        } catch (e) {
          console.error(e);
        }
        context.configuration = success.configuration;
        context.configuration.status = success.configuration.status == "enabled";
        context.configuration.Users = context.configuration.Users.split(",").join("\n");
        context.view.isLoaded = true;
      },
      function(error) {
        console.error(error);
          context.view.isLoaded = true;
      }
    );
  },
  toggleStatus() {
    this.configuration.status = !this.configuration.status;
    this.$forceUpdate();
  },
  saveSettings(type) {
    var context = this;
    var settingsObj = {
      action: "configuration",
      status: context.configuration.status
        ? "enabled"
        : "disabled",
        Webaccess: context.configuration.Webaccess,
        Users: context.configuration.Users.split("\n").join(",")
    };
    context.loaders = true;
    context.errors = context.initErrors();
    nethserver.exec(
      ["nethserver-transmission/validate"],
      settingsObj,
      null,
      function(success) {
        context.loaders = false;
    
        // notification
        nethserver.notifications.success = context.$i18n.t(
          "settings.settings_updated_ok"
        );
        nethserver.notifications.error = context.$i18n.t(
          "settings.settings_updated_error"
        );
        // update values
        nethserver.exec(
          ["nethserver-transmission/update"],
          settingsObj,
          function(stream) {
            console.info("ddclient", stream);
          },
          function(success) {
            context.getSettings();
          },
          function(error, data) {
            console.error(error, data);
          },
          true //sudo
        );
      },
      function(error, data) {
        var errorData = {};
        context.loaders = false;
        context.errors = context.initErrors();
        try {
          errorData = JSON.parse(data);
          for (var e in errorData.attributes) {
            var attr = errorData.attributes[e];
            context.errors[attr.parameter].hasError = true;
            context.errors[attr.parameter].message = attr.error;
            context.errors[attr.parameter].value = attr.value;
          }
        } catch (e) {
          console.error(e);
        }
    },
      true // sudo
  );
  },
  toggleAdvancedMode() {
    this.advanced = !this.advanced;
    this.$forceUpdate();
  }
}
};
</script>

<style>
</style>
