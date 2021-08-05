<template>
  <b-container>
    <b-row>
      <b-col sm="9" align-self="center">
        <div v-if="User">
          <p>Hi {{User}}</p>
        </div>
        <div>
            <form @submit.prevent="submit">
              <div>
                <textarea name="description" v-model="form.description" placeholder="Description..."></textarea>
              </div>
              <button type="submit"> Submit</button>
            </form>
        </div>

        <div v-if="Items">
          <ul>
            <li v-for="item in Items">
              <div>
                <p>{{item.description}} <hr> <a href="">Done</a> | <span>Edit</span> | <span @click="DeleteItem(item._id)">Remove</span></p>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          No items to show...
        </div>

      </b-col>
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
    ...mapActions(["CreateItem", "GetItems", "DeleteItem"]),
    ...mapMutations(["editItem"]),
    async submit() {
      try {
        await this.CreateItem(this.form);
      } catch (error) {
        throw "Sorry you can't make an item now!"
      }
    },
  },
};
</script>
