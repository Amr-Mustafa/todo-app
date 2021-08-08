<template>
  <b-container>
    <b-row>
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Items</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input name="description" v-model="form.description" placeholder="Description...">
            </td>
            <td>
              <b-button variant="success" @click="submit">Submit</b-button>
            </td>
          </tr>
          <tr v-for="(item, index) in Items" :key="index">
            <td>
              <input style="border: 0" v-model="item.description">
            </td>
            <td>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-warning btn-sm" @click="UpdateItem({_id: item._id, description: item.description})">Update</button>
                <button type="button" class="btn btn-danger btn-sm" @click="DeleteItem(item._id)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </b-row>
  </b-container>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import store from '../store'

export default {
  name: 'Items',
  components: {
    
  },
  data: function() {
    return {
      form: {
        description: '',
      },
    }
  },
  created: function () {
    this.GetItems()
  },
  computed: {
    ...mapGetters({Items: "StateItems", User: "StateUser"}),
  },
  methods: {
    ...mapActions(["CreateItem", "GetItems", "DeleteItem", "UpdateItem"]),
    ...mapMutations(["editItem"]),
    async submit() {
      try {
        if (this.form.description !== '') {
          await this.CreateItem(this.form);
        }
      } catch (error) {
        throw "Sorry you can't make an item now!"
      }
      this.form.description = ''
    },
  },
};
</script>
