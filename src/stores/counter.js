import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import { affixProps } from 'element-plus'
import {api} from '../boot/api'
export const useCartStore = defineStore('cart', () => {
  const cart = reactive({
  })
  function addCart(params) {
    let id = params.id
    if (cart[id]) {
      cart[id].push(params.item)
    }else{
      cart[id] = [params.item]
    }
  }
  function setCart(params) {
    let size = params.length
    for (let i = 0; i < size; i++) {
      cart[i] = params[i].items
    }
  }
  function finishFood(deskId,foodId){
    let size = cart[deskId].length
    let orderId = cart[deskId][0].orderId
    for (let i = 0; i < size; i++) {
      if(cart[deskId][i].id == foodId){
        cart[deskId][i].finish = true
        api.post('/updateorder',{orderId:orderId,items:cart[deskId]})
        break
        
      }
    }
  }
  function removeFood(deskId,foodId){
    let size = cart[deskId].length
    for (let i = 0; i < size; i++) {
      if(cart[deskId][i].id == foodId){
        cart[deskId].splice(i,1)
        api.post('/updateorder',{orderId:orderId,items:cart[deskId]})

        break
      }

    }
  }
  function finishOrder(orderId){
    console.log('==========',orderId);
    let size = cart.length;
    api.get('/finishorder?'+new URLSearchParams({orderId:orderId}))
    .then(res=>{
        window.location.reload()
    })
    // for (let i = 0; i < size; i++) {
    //   console.log(cart[i][0].orderId);
    //   if(cart[i][0].orderId == orderId){
    //     cart.splice(i,1)
    //     .then(res=>{
    //       console.log(1234);
    //     })
    //   }
    // }
  }

  return { cart,addCart,setCart,finishFood ,removeFood,finishOrder}
})

export const useOrderStore = defineStore('order', () => {
  const order = reactive({
    1:[
      {id:1,name:'商品1',price:100,count:1,finished:true},
      {id:2,name:'商品2',price:100,count:1,finished:true},
      {id:3,name:'商品3',price:100,count:1,finished:true},
    ],
    2:[
      {id:1,name:'商品1',price:100,count:1,finished:true},
      {id:2,name:'商品2',price:100,count:1,finished:true},
      {id:3,name:'商品3',price:100,count:1,finished:true},
    ]
  })
  return { order}
})