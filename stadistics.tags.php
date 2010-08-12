<?php
/*
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function createTagCloudStyle($max, $count, $initialSize = 10, $maxSize = 100) {
	$style = 'font-size: ';
	
	$size =  $initialSize + ((int)(($maxSize - $initialSize) * ($count / $max)));
	
	$style .= $size . 'px;';
	
	return $style;
}
?>
<html>
	<head>
		<title>Stadistics of Google Code</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
	</head>
	<body>
		<h1>Stadistics of Google Code</h1>
		<ul>
			<li><a href="#tag_cloud">Tag cloud</a></li>
			<li><a href="#top_ten">Top 10 tags</a></li>
			<li><a href="#list_tags">List tags</a></li>
			<!--<li><a href="#list_projects">List projects</a></li>-->
		</ul>
		
		
		<?php
		$db = new PDO('sqlite:crawler.db');
		$result = $db->query('PRAGMA cache_size = 8000');
		$result = $db->query('PRAGMA synchronous=OFF');
		?>
		
		
		<h2><a name="tag_cloud">TAG CLOUD</a></h2>
		<?php
		$result = $db->query("SELECT * FROM labels_count ORDER BY count DESC LIMIT 1");
			
		$count = $result->fetchAll();
		$count = $count[0]['count'];
		
		$result = $db->query("SELECT * FROM labels_count ORDER BY label ASC");
		
		$rows = $result->fetchAll();
		
		echo "<p>";
		foreach ($rows as $row)
		{
			$style = createTagCloudStyle($count, $row['count']);
			echo '<a href="#tag_' . $row['id'] . '" style="' . $style . '" title="' . $row['count'] . '">' . $row['label'] . '</a> ';
		}
		echo "</p>";
		
		?>
		
		
		<h2><a name="top_ten">TOP 10 TAGS</a></h2>
		<?php
		$result = $db->query("SELECT * FROM labels_count ORDER BY count DESC LIMIT 10");
			
		$rows = $result->fetchAll();
		
		echo "<ol>";
		foreach ($rows as $row) {
			echo "<li><a href='#tag_" . $row['id'] . "'>" . $row['label'] . " - " . $row['count'] . "</a></li>";
		}
		echo "</ol>";
		?>
		
		
		<h2><a name="list_tags">LIST TAGS</a></h2>
		<h3>TAG: PROJECT_1, PROJECT_2, ... PROJECT_N</h3>
		<?php
		$result = $db->query("SELECT id, label
			FROM labels AS t1 ORDER BY label ASC");
		$rows = $result->fetchAll();
		
		foreach ($rows as $row) {
			echo "<p>";
			echo "<b><a name='tag_" . $row['id'] . "'>" . $row['label'] . "</a>:</b> ";
			
			$result = $db->query("SELECT * FROM project WHERE id IN (SELECT id_project FROM project_labels WHERE id_label = " . $row['id'] . ");");
			$rows2 = $result->fetchAll();
			
			foreach ($rows2 as $row2) {
				echo "<a href='stadistics.projects.output.html#project_" . $row2['id'] . "'>" . $row2['name'] . "</a>, ";
			}
			
			echo "</p>";
		}
		?>
		
		
		<!--<h2><a name="list_projects">LIST PROJECTS</a></h2>
		<h3>PROJECT: TAG_1, TAG_2, ... TAG_N</h3>-->
		<?php
		/*
		$result = $db->query("SELECT *
			FROM project AS t1 ORDER BY name ASC");
		$rows = $result->fetchAll();
		
		foreach ($rows as $row) {
			echo "<p>";
			echo "<b><a name='project_" . $row['id'] . "'><a href='http://code.google.com" . $row['href'] . "'>" . $row['name'] . "</a></a>: </b>";
			
			$result = $db->query("SELECT * FROM labels WHERE id IN (SELECT id_label FROM project_labels WHERE id_project = " . $row['id'] . ");");
			$rows2 = $result->fetchAll();
			
			foreach ($rows2 as $row2) {
				echo "<a href='#tag_" . $row2['id'] . "'>" . $row2['label'] . "</a>, ";
			}
			
			echo "</p>";
		}
		*/
		?>
	</body>
</html>
