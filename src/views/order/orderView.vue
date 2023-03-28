<template>
    <div v-if="cart">
        <h1>Order</h1>
        <div v-for="desk_id in Object.keys(cart)" :key="desk_id">
            <div class=" tw-m-4 tw-rounded-xl tw-border tw-shadow tw-mt-4" >
                <el-collapse v-model="activeNames[desk_id]">
                    <el-collapse-item name="1">
                        <template #title class="tw-flex">
                            <span class="tw-font-bold tw-ml-3 tw-text-2xl tw-flex-1">桌号{{ cart[desk_id][0].tableNumber }}</span>
                            <el-button class="tw-mr-3 tw-ml-3" type="primary" 
                            @click="finishOrderFromCart(cart[desk_id][0].orderId)">完成订单</el-button>
                        </template>

                        <div v-for="item in cart[desk_id]" :key="item.id" class=" tw-space-y-4">
                            <div class="tw-border tw-m-3 tw-shadow tw-rounded">
                                <div class="tw-flex tw-m-3">
                                    <span class=" tw-font-bold tw-flex-1">
                                        菜名：{{ item.name }}
                                    </span>
                                    <el-checkbox v-if="!item.finish" v-model="item.finish" class="tw-mr-2"></el-checkbox>
                                    <el-checkbox v-else  v-model="item.finish" class="tw-mr-2" disabled></el-checkbox>
                                </div>
                                <div class=" tw-m-3 tw-gray-400">
                                  价格  {{ item.price }}
                                </div>
                                <span class="tw-m-3">
                                  份额  {{ item.count }}
                                </span>
                                <div class=" tw-flex tw-flex-row-reverse tw-mb-3 tw-mr-4">
                                    <!-- <el-button class="tw-mb-3" type="danger" @click="removeFoodFromCart(desk_id,item.id)">删除</el-button> -->
                                    <el-button class="tw-mb-3" type="primary" @click="finishFoodStatus(desk_id,item.id)">确认</el-button>
                                </div>
                            </div>
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '../../stores/counter';
import {api} from "../../boot/api"
import { ElMessage } from 'element-plus';
const cartStore = useCartStore();
const cart = cartStore.cart;
const activeNames = ref([].fill('1', 0, Object.keys(cart).length));
api.get('/getallorder').then(r=>{
        let data = r.data
        cartStore.setCart(data)
      })

const finishFoodStatus = (desk_id,foodid) => {
    cartStore.finishFood(desk_id,foodid);
    console.log(cart);
    ElMessage({
        message: '已完成',
        type: 'success'
      });

}
const removeFoodFromCart = (desk_id,foodid) => {
    cartStore.removeFood(desk_id,foodid);
    console.log(cart);
    ElMessage({
        message: '已删除',
        type: 'success'
      });
}
const finishOrderFromCart = (orderId) =>{
    console.log(orderId);
    cartStore.finishOrder(orderId);
    console.log(cart);
}

</script>