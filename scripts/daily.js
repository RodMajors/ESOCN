// server.js
import express from 'express'
import cors from 'cors';
const app = express();
app.use(cors())
const port = 5000;

const PledgeList1 = [
    "Spindleclutch II",
    "The Banished Cells I",
    "Fungal Grotto II",
    "Spindleclutch I",
    "Darkshade Caverns II",
    "Elden Hollow I",
    "Wayrest Sewers II",
    "Fungal Grotto I",
    "The Banished Cells II",
    "Darkshade Caverns I",
    "Elden Hollow II",
    "Wayrest Sewers I"
];

const PledgeList2 = [
    "Direfrost Keep",
    "Vaults of Madness",
    "Crypt of Hearts II",
    "City of Ash I",
    "Tempest Island",
    "Blackheart Haven",
    "Arx Corinium",
    "Selene's Web",
    "City of Ash II",
    "Crypt of Hearts I",
    "Volenfell",
    "Blessed Crucible"
];

const PledgeList3 = [
    "Imperial City Prison",
    "Ruins of Mazzatun",
    "White-Gold Tower",
    "Cradle of Shadows",
    "Bloodroot Forge",
    "Falkreath Hold",
    "Fang Lair",
    "Scalecaller Peak",
    "Moon Hunter Keep",
    "March of Sacrifices",
    "Depths of Malatar",
    "Frostvault",
    "Moongrave Fane",
    "Lair of Maarselok",
    "Icereach",
    "Unhallowed Grave",
    "Stone Garden",
    "Castle Thorn",
    "Black Drake Villa",
    "The Cauldron",
    "Red Petal Bastion",
    "The Dread Cellar",
    "Coral Aerie",
    "Shipwright's Regret",
    "Earthen Root Enclave",
    "Graven Deep"
];

function getDailyPledges() {
    const startIndex1 = PledgeList1.indexOf("Spindleclutch I");
    const startIndex2 = PledgeList2.indexOf("City of Ash I");
    const startIndex3 = PledgeList3.indexOf("Imperial City Prison");

    const now = new Date();
    
    const startDate = new Date('2025-03-12T18:00:00');

    const timeDiff = now.getTime() - startDate.getTime();
    const hoursDiff = timeDiff / (1000 * 3600);
    const daysDiff = Math.floor(hoursDiff / 24);
    console.log(daysDiff)
    let rotationCount = daysDiff;
    if (now.getHours() < 18) {
        rotationCount--;
    }
    rotationCount = Math.max(0, rotationCount);

    const index1 = (startIndex1 + rotationCount) % PledgeList1.length;
    const index2 = (startIndex2 + rotationCount) % PledgeList2.length;
    const index3 = (startIndex3 + rotationCount) % PledgeList3.length;

    return {
        dailyPledges: [
            PledgeList1[index1],
            PledgeList2[index2],
            PledgeList3[index3]
        ],
        currentDate: now.toISOString()
    };
}

// API 端点
app.get('/api/daily-pledges', (req, res) => {
    const result = getDailyPledges();
    res.json(result);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});