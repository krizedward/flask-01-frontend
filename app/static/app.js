// document.addEventListener('DOMContentLoaded', function() {
//     fetch('/api/persons')
//         .then(response => response.json())
//         .then(data => {
//             const tableBody = document.querySelector('#example1 tbody');
//             data.forEach(person => {
//                 const row = document.createElement('tr');
//                 row.innerHTML = `
//                     <td>${person.id}</td>
//                     <td>${person.name}</td>
//                     <td>${person.address}</td>
//                     <td>Version</td>
//                     <td>Grade</td>
//                 `;
//                 tableBody.appendChild(row);
//             });
//         })
//         .catch(error => console.error('Error fetching person data:', error));
// });

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/persons')
        .then(response => response.json())
        .catch(error => console.error('Error fetching person data:', error));
});
