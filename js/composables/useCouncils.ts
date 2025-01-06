import {computed} from "vue";
import MiltonKeynes from "~/components/councils/MiltonKeynes.vue";
import Buckinghamshire from "~/components/councils/Buckinghamshire.vue";

export const useCouncils = () => {
    const councils = [
        new MiltonKeynesCouncil(),
        new BuckinghamshireCouncil()
    ];

    const councilSelectSchema = computed(() => {
        return councils.map(council => {
            return {
                value: council.key,
                label: council.name
            }
        })
    });

    const councilKeys = computed<Array<string>>(() => {
        return councils.map(council => council.key);
    });

    return {
        councils,
        councilSelectSchema,
        councilKeys
    }
}

export abstract class Council {
    abstract key: string;
    abstract name: string;
    abstract component: any;
}

class MiltonKeynesCouncil extends Council {
    key = 'MiltonKeynesCityCouncil';
    name = 'Milton Keynes City Council';
    component = MiltonKeynes
}

class BuckinghamshireCouncil extends Council {
    key = 'BuckinghamshireCouncil';
    name = 'Buckinghamshire Council';
    component = Buckinghamshire
}