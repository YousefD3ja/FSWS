const userCardTemplate = document.querySelector('[data-user-template]')
const userCardContainer = document.querySelector('[data-user-container]')
const searchInput = document.querySelector('[data-search]')


searchInput.addEventListener('input', (e) => {
    const value = e.target.value

    fetch('http://192.168.1.22:3030/getusers', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user: `${value}`
        })
    }).then(res => res.json()
    ).then(data => {
        userCardContainer.textContent = ''
        console.log(data)
        userArray = Array.from(data)

        console.log(userArray)
        userArray.forEach(user => {
            const card = userCardTemplate.content.cloneNode(true).children[0]
            const userLink = card.querySelector('[data-user-link]')
            const userimg = card.querySelector('[data-user-image]')
            userLink.textContent = user.name
            userLink.href = `/user/${user.name}`
            userimg.src = `${user.image}`
            userCardContainer.append(card)
        })
    })
})
searchInput.addEventListener('click', (e) => {
    const value = e.target.value
    

    fetch('http://192.168.1.22:3030/getusers', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user: `${value}`
        })
    }).then(res => res.json()
    ).then(data => {
        userCardContainer.textContent = ''
        console.log(data)
        userArray = Array.from(data)
        console.log(userArray)
        userArray.forEach(user => {
            const card = userCardTemplate.content.cloneNode(true).children[0]
            const userLink = card.querySelector('[data-user-link]')
            const userimg = card.querySelector('[data-user-image]')
            userLink.textContent = user.name
            userLink.href = `/user/${user.name}`
            userimg.src = `${user.image}`
            userCardContainer.append(card)
        })
    })
})

// if (lastvalue != value)
// {
//     console.log(lastvalue+','+value)
//     fetch('http://192.168.1.22:3030/getusers', {
//         method: "POST",
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             user: `${value}`
//         })
//     }).then(res => res.json()
//     ).then(data => {
//         console.log(data)
//         userArray = Array.from(data)
//         console.log(userArray)
//         userArray.forEach(user => {
//             const card = userCardTemplate.content.cloneNode(true).children[0]
//             const userLink = card.querySelector('[data-user-link]')
//             const userimg = card.querySelector('[data-user-image]')
//             userLink.textContent = user.name
//             userLink.href = `/user/${user.name}`
//             userimg.src = `${user.image}`
//             userCardContainer.append(card)
//         })    
//     }).then(data => console.log(data + "2"))

//     lastvalue = value
// }