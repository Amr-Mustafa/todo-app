<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Items</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.item-modal>Add Item</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Item</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in items" :key="index">
              <td @click="editItem">{{ item.description }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addItemModal" id="item-modal" title="Add a new item" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">

        <b-form-group id="form-description-group" label="Description:" label-for="form-description-input">
          <b-form-input id="form-description-input" type="text" v-model="addItemForm.description" required
                        placeholder="Enter description">
          </b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>

      </b-form>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
      addItemForm: {
        description: '',
      },
    };
  },
  methods: {
    editItem(event) {
      console.log(this.items.find((item) => item === event.target.firstChild.data));
      //this.item.description = 'afaf';
    },
    getItems() {
      const path = 'http://localhost:8000/items';
      axios.get(path)
        .then((res) => {
          this.items = res.data.items;
        })
        .catch((error) => {
          // eslint-disable-next-line
          alert(error);
        });
    },
    addItem(payload) {
      const path = 'http://localhost:8000/item';
      axios.post(path, payload)
        .then(() => {
          this.getItems();
        })
        .catch((error) => {
          alert(error);
          this.getItems();
        });
    },
    initForm() {
      this.addItemForm.description = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addItemModal.hide();
      const payload = {
        description: this.addItemForm.description,
      };
      this.addItem(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addItemModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getItems();
  },
};
</script>
