import axios from "axios";

const state = {
  user: null,
  items: null,
};

const getters = {
  isAuthenticated: (state) => !!state.user,
  StateItems: (state) => state.items,
  StateUser: (state) => state.user.email,
};

const actions = {
  async Register({ dispatch }, form) {
    await axios.post('register', form)
    let UserForm = new FormData()
    UserForm.append('email', form.email)
    UserForm.append('password', form.password)
    await dispatch('LogIn', UserForm)
  },

  async LogIn({ commit }, user) {
    let response = await axios.post("login", user);
    await commit("setUser", {
      "email": user.get("email"),
      "jwt_token": response.data,
    });
  },

  async CreateItem({ dispatch }, item) {
    let config = {
      headers: {
        "Authorization": "Bearer " + state.user.jwt_token
      }
    }
    await axios.post("item", item, config);
    return await dispatch("GetItems");
  },

  async DeleteItem({ dispatch }, item) {
    let config = {
      headers: {
        "Authorization": "Bearer " + state.user.jwt_token,
      },
      data: {
        _id: item,
      },
    }
    await axios.delete("item", config);
    return await dispatch("GetItems");
  },

  async GetItems({ commit }) {
    let config = {
      headers: {
        "Authorization": "Bearer " + state.user.jwt_token
      }
    }
    let response = await axios.get("items", config);
    commit("setItems", response.data);
  },

  async LogOut({ commit }) {
    let user = null;
    commit("logout", user);
  },
};

const mutations = {
  setUser(state, user) {
    state.user = user;
  },

  setItems(state, items) {
    state.items = items;
  },

  logout(state, user) {
    state.user = user;
  },

  editItem(state, payload) {
    state.items[payload.index].description = payload.description;
  }
};

export default {
  state,
  getters,
  actions,
  mutations,
};