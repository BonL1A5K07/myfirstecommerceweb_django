var updateBtns = document.getElementsByClassName('update-cart')

for (var i =0 ; i < updateBtns.length ; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'action:',action)
        
        console.log('USER:',user)
        if (user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

// // Dạng JSON
// {
//     "1": { "quantity": 1 },
//     "2": { "quantity": 5 },
//     "3": { "quantity": 10 }
// }
// >> đây là dạng javascript
// cart = { 
//     1: {'quantity': 1},
//     2: {'quantity': 5},
//     3: {'quantity': 10},
// }


function addCookieItem(productId, action){
    console.log('Not logged in..')

    if(action == 'add'){
        if(cart[productId] == undefined){ // ko ton tai thi set = 1
            cart[productId] = {'quantity':1}  //id1 : {'quantity'} :1
        }else{
            cart[productId]['quantity'] += 1 //id1 : {'quantity'}' :2
        }
    }
    
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        
        if(cart[productId]['quantity'] <= 0 ){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    
    console.log('Cart:',cart)
    //cart sẽ bị ghi đè lên khi vào cart (bên main.html là tạo cart dạng js rỗng)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload() 
   
}


function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data....')
    var url = '/update_item/'

    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then ((data) => {
        location.reload()
        console.log('data:',data)
        
    });
}