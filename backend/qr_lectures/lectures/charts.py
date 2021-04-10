from .models import Lecture


class Dataset():
    data = []
    raw_data = ''
    color = ''
    title = ''

    def __init__(self, data):
        self.data = self.get_dataset(data)
        self.raw_data = ','.join(str(x) for x in self.data)

    def get_dataset(self, data):
        return data


class Chart():
    datasets_classes = []

    datasets = []
    labels = []
    titles = []

    raw_labels = ''
    raw_titles = ''

    value = None

    icon = ''

    _data = []

    def __init__(self, queryset):
        self._data = queryset
        self.datasets = []
        for d_class in self.datasets_classes:
            self.datasets.append(d_class(self._data))
        
        self.value = self.get_value()
        self.raw_labels = ','.join(str(x) for x in self.get_labels())
        print (self.get_labels())
  

    def get_titles(self):
        return self.titles

    def get_labels(self):
        return self.labels

    def get_data(self):
        return self._data

    def get_value(self):
        return self.value


class EngagementDataSet(Dataset):
    color = 'secondary'
    title = 'Engagement'

    def get_dataset(self, data):
        lectures = data
        temp = []
        for lec in lectures:
            temp.append(round(lec.get_engagement(),2))

        return temp


class EngagementAvgDataSet(Dataset):
    color = 'info'
    title = 'Media'

    def get_dataset(self, data):
        lectures = data

        cumulative = []
        sum = 0
        for i in range(0, len(data)):
            sum += lectures[i].get_engagement()
            cumulative.append(sum)

        temp = []
        for i in range(0, len(cumulative)):
            temp.append(round(cumulative[i]/(i+1), 2))

        return temp


class EngagementChart(Chart):
    datasets_classes = [EngagementDataSet, EngagementAvgDataSet]
    icon = 'trending_up'

    def get_labels(self):
        labels = []
        for l in self._data:
            labels.append(l.name)
        return labels

    def get_data(self):
        return Lecture.objects.get_latest(months=2)

    def get_value(self):
        return round(self.datasets[1].data[-1],2)


class StudCountDataSet(Dataset):
    color = 'secondary'
    title = '#Studenti'

    def get_dataset(self, data):
        lectures = data
        temp = []
        for lec in lectures:
            temp.append(len(lec.get_students()))

        return temp



class StudAvgDataSet(Dataset):
    color = 'info'
    title = 'Media'

    def get_dataset(self, data):
        lectures = data

        cumulative = []
        sum = 0
        for i in range(0, len(data)):
            sum += len(lectures[i].get_students())
            cumulative.append(sum)

        temp = []
        for i in range(0, len(cumulative)):
            temp.append(round(cumulative[i]/(i+1)))

        return temp


class StudCountChart(Chart):
    datasets_classes = [StudCountDataSet, StudAvgDataSet]
    icon = 'group'

    def get_labels(self):
        labels = []
        for l in self._data:
            labels.append(l.name)
        return labels

    def get_data(self):
        return Lecture.objects.get_latest(months=2)

    def get_value(self):
        return round(self.datasets[1].data[-1])