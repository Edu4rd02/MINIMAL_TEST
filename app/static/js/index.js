// Funciones de Carrito de Compras con Persistencia

// Función para guardar el carrito en localStorage
function saveCartToLocalStorage(cart) {
    localStorage.setItem('shoppingCart', JSON.stringify(cart));
}

// Función para cargar el carrito desde localStorage
function loadCartFromLocalStorage() {
    const savedCart = localStorage.getItem('shoppingCart');
    return savedCart ? JSON.parse(savedCart) : [];
}

// Variable global para almacenar los productos del carrito
let cart = loadCartFromLocalStorage();

// Función para renderizar los items del carrito
function renderCartItems() {
    const cartItemsContainer = document.querySelector('.cart-items');
    const cartTotalElement = document.querySelector('.total-price');
    
    // Limpiar contenido actual del carrito
    cartItemsContainer.innerHTML = '';
    
    // Calcular total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // Renderizar cada item del carrito
    cart.forEach((item, index) => {
        const cartItemElement = document.createElement('div');
        cartItemElement.classList.add('cart-item');
        cartItemElement.innerHTML = `
            <img src="${item.image}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-details">
                <h3>${item.name}</h3>
                <p class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</p>
                <div class="cart-item-quantity">
                    <button class="quantity-btn decrease" data-index="${index}">-</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn increase" data-index="${index}">+</button>
                </div>
            </div>
            <button class="cart-item-remove" data-index="${index}">&times;</button>
        `;
        cartItemsContainer.appendChild(cartItemElement);
    });
    
    // Actualizar total
    cartTotalElement.textContent = `$${total.toFixed(2)}`;
    
    // Guardar en localStorage
    saveCartToLocalStorage(cart);
}

// Función para agregar un producto al carrito
function addToCart(name, price, image) {
    // Buscar si el producto ya existe en el carrito
    const existingItem = cart.find(item => item.name === name);
    
    if (existingItem) {
        // Si existe, aumentar la cantidad
        existingItem.quantity += 1;
    } else {
        // Si no existe, agregar nuevo item
        cart.push({
            name: name,
            price: price,
            quantity: 1,
            image: image
        });
    }
    
    renderCartItems();
    openCart();
}

// Función para abrir el carrito
function openCart() {
    const cartPanel = document.querySelector('.cart-panel');
    const cartOverlay = document.querySelector('.cart-overlay');
    
    cartPanel.classList.add('open');
    cartOverlay.classList.add('active');
}

// Función para cerrar el carrito
function closeCart() {
    const cartPanel = document.querySelector('.cart-panel');
    const cartOverlay = document.querySelector('.cart-overlay');
    
    cartPanel.classList.remove('open');
    cartOverlay.classList.remove('active');
}

// Función para manejar cambios en la cantidad
function handleQuantityChange(index, change) {
    const item = cart[index];
    item.quantity += change;
    
    if (item.quantity <= 0) {
        // Eliminar item si la cantidad es 0 o menos
        cart.splice(index, 1);
    }
    
    renderCartItems();
}

// Función para eliminar un item del carrito
function removeCartItem(index) {
    cart.splice(index, 1);
    renderCartItems();
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Botón de carrito
    const cartIcon = document.querySelector('.cart-icon');
    cartIcon.addEventListener('click', openCart);
    
    // Botón de cerrar carrito
    const closeCartBtn = document.querySelector('.close-cart');
    closeCartBtn.addEventListener('click', closeCart);
    
    // Overlay del carrito
    const cartOverlay = document.querySelector('.cart-overlay');
    cartOverlay.addEventListener('click', closeCart);
    
    // Botones de agregar al carrito
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const productCard = e.target.closest('.product-card');
            const name = productCard.querySelector('.product-title').textContent;
            const price = parseFloat(productCard.querySelector('.product-price span').textContent.replace('$', ''));
            const image = productCard.querySelector('.product-img img').src;
            
            addToCart(name, price, image);
        });
    });
    
    // Delegación de eventos para botones de cantidad y eliminación
    const cartItemsContainer = document.querySelector('.cart-items');
    cartItemsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('quantity-btn')) {
            const index = e.target.getAttribute('data-index');
            const change = e.target.classList.contains('increase') ? 1 : -1;
            handleQuantityChange(Number(index), change);
        }
        
        if (e.target.classList.contains('cart-item-remove')) {
            const index = e.target.getAttribute('data-index');
            removeCartItem(Number(index));
        }
    });
    
    // Renderizar items existentes al cargar
    renderCartItems();
});

// Botón de pago (checkout)
document.querySelector('.checkout-btn').addEventListener('click', () => {
    alert('Gracias por tu compra. Próximamente la funcionalidad de pago.');
    // Aquí puedes agregar la lógica de redireccionamiento a pasarela de pago
});