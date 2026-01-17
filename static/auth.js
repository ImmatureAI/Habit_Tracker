const habitList = document.getElementById('habitList');
const add = document.getElementById('addNewHabit');

function openModal(){
    document.getElementById('habitModal').style.display = 'flex';
}

function closeModal(){
    document.getElementById('habitModal').style.display = 'none';
}

function startup(){
    for(let i = 0; i < habits.length; i++){
        const habit = document.createElement('div');
        habit.setAttribute('class', 'habit');
        habit.setAttribute('id', `habit_${habits[i][1]}`)

        const checkContainer = document.createElement('div');
        checkContainer.setAttribute('class', 'habitCheckContainer');
        checkContainer.setAttribute('id', 'checkContainer_'+i);
        
        const habitTitle = document.createElement('div');
        habitTitle.setAttribute('class', 'habitTitle');
        habitTitle.innerText = habits[i][0];

        for(let j = 0; j < daysInMonth; j++){
            const checkBox = document.createElement('div');
            checkBox.setAttribute('class', 'habitCheckbox');
            checkBox.setAttribute('id', `check_${habits[i][1]}_${j+1}`);
            checkBox.style.backgroundColor = "red";
            checkContainer.appendChild(checkBox);
        }
        habit.appendChild(habitTitle);
        habit.appendChild(checkContainer);
        habitList.appendChild(habit);
    }

    habitLog.forEach(row => {
        let habitid = row[0];
        let date = parseInt(row[1].split('-')[2]);
        const checkBox = document.getElementById(`check_${habitid}_${date}`)
        checkBox.style.backgroundColor = "green";       
    });
}
startup();