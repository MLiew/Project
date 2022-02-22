## 北航GPA计算器 GPA Calculator of Beihang University
北京航空航天大学的GPA计算方法为：
 <table>
  <tr>
    <th>制度System</th>
    <th>计算公式Formula</th>
  </tr>
  <tr>
<td>百分制Percentile</td>
<td>  4-3 * (100-X)^2 / 1600
    </td>
  </tr>
  <tr>
    <td rowspan="5">五级制Five level</td>
    <td>优秀Excellent：4</td>
  </tr>
  <tr>
    <td>良好Good：3.5</td>
  </tr>
  <tr>
    <td>中等Average：2.8</td>
  </tr>
  <tr>
    <td>及格Pass：1.7</td>
  </tr>
    <tr>
    <td>不及格Failed：0</td>
  </tr>
    <tr>
    <td>两级制Pass-fail</td>
    <td>不计入GPA，但计入总学分Not included in the GPA</td>
  </tr>
</table> 

</br>
这里使用Python程序来编写这个GPA计算机，下图为GUI界面. Python is used to write this program, the UI is shown as below.

![GPA Calculator](https://img-blog.csdnimg.cn/20200825125713485.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NTYwNjIw,size_16,color_FFFFFF,t_70#pic_center)
- System：计分制度，选择百分制（Percentile）和五级制(5-point grading)；
- Score：分数，百分制为分数，五级制为等级；
- Point：学分。


1. 在使用时，选择对应的计分制度，输入分数和学分，点击"Add to list"按钮或敲下键盘上的Enter/Return键，即可输入分数。（*五级制的要输入“优秀”、“良好”等中文等级。）
2. 在输入完所有的分数以后，点击"Calculate"按钮，GPA分数便会计算完成。
3. 需要再次进行计算时，可点击"Recalculate"按钮，前面所输入的所有成绩将会清除。
4. 注意：此程序并没有添加删除的功能，所以在使用的时候，需要小心输入成绩。若有需要，可自行修改代码。

由于代码略长，只显示较为重要的部分代码（计算GPA的类）：

```python
class GPA():
    """
    This is a class that calculates beihang gpa, with its own unique calculation method.
    """
    
    @classmethod
    def get_gpa(cls, score):
        if score<60:
            print("Failed")
            gpa_score = 0
        else:
            gpa_score = 4 - 3 * np.power((100-score),2) / 1600
        return gpa_score

    @classmethod
    def cal_score(cls, score_arr, point_arr):
        products = np.sum([score * point for score, point in zip(score_arr, point_arr)])
        sum_point = np.sum(point_arr)
        gpa = products/sum_point
        return gpa

class FourGrade(GPA):
    @classmethod
    def convert_mark(cls, score):
        """
        Convert the four grading into gpa system, e.g. 优秀=4， 良好=3.5.
        Return:
            gpa_score(float): The gpa grading mark.
        """
        if score == "优秀":
            gpa_score = 4
        elif score == "良好":
            gpa_score = 3.5
        elif score == "中等":
            gpa_score = 2.8
        elif score == "及格":
            gpa_score = 1.7
        elif score == "不及格":
            gpa_score = 0
        else:
            return False
        return gpa_score
```
