package main

import (
	"encoding/json"
	"fmt"
	"io"
	"math"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"sync/atomic"
	"time"
)

const (
	// tileURL       = "http://webst01.is.autonavi.com/appmaptile?style=6&x=%d&y=%d&z=%d"
	// outputDir     = "gd_tiles1"
	tileURL       = "https://data.mars3d.cn/terrain/%d/%d/%d.terrain"
	outputDir     = "terrain"
	maxGoroutines = 5000 // 最大协程数量
)

var (
	sem         = make(chan struct{}, maxGoroutines) // 控制并发数量
	client      = &http.Client{}                     // 默认 HTTP 客户端支持 HTTP/2
	tileCounter int32                                // 下载计数器
	startTime   time.Time
)

// downloadTile 下载瓦片并保存到本地
func downloadTile(z, x, y int, wg *sync.WaitGroup) {
	fmt.Println(1111111233)
	defer wg.Done()
	sem <- struct{}{} // 获取信号
	defer func() { <-sem }()

	// 更新计数器
	total := atomic.AddInt32(&tileCounter, 1)
	if total%1000 == 0 {
		elapsed := time.Since(startTime)
		fmt.Printf("Downloaded %d tiles, elapsed time: %v\n", total, elapsed)
	}
	fmt.Println(11111112)

	// 创建目录
	zoomDir := filepath.Join(outputDir, fmt.Sprintf("%d", z))
	levelDir := filepath.Join(zoomDir, fmt.Sprintf("%d", x))
	tileFile := filepath.Join(levelDir, fmt.Sprintf("%d.terrain", y))

	if _, err := os.Stat(tileFile); err == nil {
		fmt.Printf("Tile %d-%d-%d already exists, skipping.\n", z, x, y)
		return
	}
	if err := os.MkdirAll(levelDir, os.ModePerm); err != nil {
		fmt.Printf("Error creating directory for tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}

	url := fmt.Sprintf(tileURL, z, x, y)

	// 创建请求
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Printf("Error creating request for tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}
	fmt.Println(1111111)

	// 设置请求头
	// for key, value := range headers {
	// 	req.Header.Set(key, value)
	// }

	// 发起请求
	fmt.Println(req)
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Error downloading tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		// fmt.Printf("Failed to download tile %d-%d-%d, status code: %d\n", z, x, y, resp.StatusCode)
		return
	}

	// 保存瓦片文件
	file, err := os.Create(tileFile)
	if err != nil {
		// fmt.Printf("Error creating file for tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		// fmt.Printf("Error saving tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}

	// fmt.Printf("Downloaded tile %d-%d-%d\n", z, x, y)
}

func degreesToRadians(degrees float64) float64 {
	return degrees * math.Pi / 180.0
}

// 地理坐标转瓦片坐标的转换函数
func latLonToTile(lat, lon float64, z int) (int, int) {
	// 将经纬度转为墨卡托坐标
	x := (lon + 180.0) / 360.0 * math.Pow(2, float64(z))
	y := (1 - math.Log(math.Tan(degreesToRadians(lat))+1/math.Cos(degreesToRadians(lat)))/math.Pi) / 2 * math.Pow(2, float64(z))

	// 瓦片坐标需向下取整
	xTile := int(math.Floor(x))
	yTile := int(math.Floor(y))

	return xTile, yTile
}

// 定义结构体
type TileRange struct {
	EndX   int `json:"endX"`
	EndY   int `json:"endY"`
	StartX int `json:"startX"`
	StartY int `json:"startY"`
}

func main() {
	var wg sync.WaitGroup
	startTime = time.Now()

	// 定义中国范围经纬度
	// minLat := 3.0   // 中国南部的纬度
	// maxLat := 53.0  // 中国北部的纬度
	// minLon := 73.0  // 中国西部的经度
	// maxLon := 135.0 // 中国东部的经度

	for z := 6; z <= 6; z++ { // Zoom levels
		// fmt.Println(111)
		// // [
		// // 	{ "endX": 0, "endY": 1, "startX": -1, "startY": 0 },
		// // 	{ "endX": 1, "endY": 1, "startX": 1, "startY": 0 }
		// // ]
		// minX, minY := -1, 0
		// maxX, maxY := 0, 1

		data := ` [
        { "endX": 31, "endY": 65, "startX": -2, "startY": 0 },
        { "endX": 63, "endY": 65, "startX": 32, "startY": 0 },
        { "endX": 95, "endY": 65, "startX": 64, "startY": 0 },
        { "endX": 127, "endY": 65, "startX": 96, "startY": 0 }
      ]`

		// 解析 JSON
		var tiles []TileRange
		err := json.Unmarshal([]byte(data), &tiles)
		if err != nil {
			fmt.Println("JSON 解析错误:", err)
			return
		}

		// 输出结果
		for i, tile := range tiles {
			fmt.Printf("Tile %d: startX=%d, startY=%d, endX=%d, endY=%d\n", i, tile.StartX, tile.StartY, tile.EndX, tile.EndY)
			for x := tile.StartX; x <= tile.EndX; x++ {
				fmt.Println(1112)
				for y := tile.StartY; y <= tile.EndY; y++ {
					wg.Add(1)
					go downloadTile(z, x, y, &wg)
				}
			}
		}

		// for x := minX; x <= maxX; x++ {
		// 	fmt.Println(1112)
		// 	for y := minY; y <= maxY; y++ {
		// 		wg.Add(1)
		// 		go downloadTile(z, x, y, &wg)
		// 	}
		// }
	}

	// for z := 0; z <= 0; z++ {
	// 	for x := 0; x < (1 << z); x++ {
	// 		for y := 0; y < (1 << z); y++ {
	// 			wg.Add(1)
	// 			go downloadTile(z, x, y, &wg)
	// 		}
	// 	}
	// }

	wg.Wait()
	fmt.Println("All tiles downloaded successfully.")
}
